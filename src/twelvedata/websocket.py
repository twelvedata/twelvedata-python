import time
import threading
import json
import logging
import queue

SELF_HEAL_TIME = 1
MAX_QUEUE_SIZE = 12000


class TDWebSocket:
    def __init__(self, ctx):
        self.apikey = ctx.apikey
        self.defaults = ctx.defaults

        self.ws = None
        self.ready = False
        self.event_receiver = None
        self.event_handler = None
        self.last_queue_warning_time = 0
        self.subscribed_symbols = set()

        self.logger = self.set_default_logger()
        self.symbols = self.set_default_symbols()
        self.events = self.set_default_events_queue()
        self.on_event = self.set_default_event_function()

        self.url = "wss://ws.twelvedata.com/v1/quotes/price?apikey={}".format(self.apikey)

        EventHandler(self).start()

    def set_default_logger(self):
        if "logger" in self.defaults:
            return self.defaults["logger"]

        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger = logging.getLogger("ws-twelvedata")
        if "log_level" in self.defaults:
            log_level = self.defaults["log_level"]
            if log_level == "debug":
                logger.setLevel(logging.DEBUG)
            elif log_level == "info":
                logger.setLevel(logging.INFO)
            else:
                logger.setLevel(logging.NOTSET)
        logger.addHandler(handler)
        return logger

    def set_default_symbols(self):
        if "symbols" in self.defaults:
            if isinstance(self.defaults["symbols"], str):
                return {self.defaults["symbols"].upper()}
            return set(self.normalize_symbols(self.defaults["symbols"]))
        return set()

    def set_default_events_queue(self):
        if "max_queue_size" in self.defaults:
            return queue.Queue(maxsize=self.defaults["max_queue_size"])
        return queue.Queue(maxsize=MAX_QUEUE_SIZE)

    def set_default_event_function(self):
        if "on_event" in self.defaults:
            if not callable(self.defaults["on_event"]):
                raise ValueError("Parameter 'on_event' must be a function")
            else:
                return self.defaults["on_event"]
        return None

    def connect(self):
        self.logger.info("Connecting...")
        self.ready = False
        self.subscribed_symbols = set()

        if self.ws:
            self.ws.close()
            time.sleep(1)

        while True:
            try:
                self.refresh_websocket()
                break
            except Exception as e:
                self.logger.error("Cannot connect: {}. Retrying...".format(e))
                time.sleep(SELF_HEAL_TIME)

    def disconnect(self):
        self.ready = False
        self.subscribed_symbols = set()

        if self.ws:
            self.ws.close()
            time.sleep(1)

    def keep_alive(self):
        self.logger.info('Method keep_alive is deprecated, use heartbeat method instead')
        self.heartbeat()

    def heartbeat(self):
        if not self.ready:
            return

        try:
            self.ws.send('{"action": "heartbeat"}')
        except Exception as e:
            self.logger.error("Error calling heartbeat method: {}".format(e))

    def refresh_websocket(self):
        self.event_receiver = EventReceiver(self)
        self.event_receiver.start()

    def self_heal(self):
        time.sleep(SELF_HEAL_TIME)
        self.connect()

    def on_connect(self):
        self.ready = True
        self.update_subscription_symbols()

    def on_queue_full(self):
        if time.time() - self.last_queue_warning_time > 1:
            self.logger.error("Event queue is full. New events are not added.")
            self.last_queue_warning_time = time.time()

    def subscribe(self, symbols):
        if isinstance(symbols, str):
            symbols = [symbols.upper()]
        else:
            symbols = self.normalize_symbols(symbols)

        self.symbols = self.symbols | set(symbols)
        self.update_subscription_symbols()

    def unsubscribe(self, symbols):
        if isinstance(symbols, str):
            symbols = [symbols.upper()]
        else:
            symbols = self.normalize_symbols(symbols)

        self.symbols = self.symbols - set(symbols)
        self.update_subscription_symbols()

    def reset(self):
        self.symbols = set()
        self.subscribed_symbols = set()
        self.ws.send('{"action": "reset"}')

    def update_subscription_symbols(self):
        if not self.ready:
            return

        # Subscribe
        new_symbols = self.symbols - self.subscribed_symbols
        if len(new_symbols) > 0:
            self.logger.debug("New symbols: {}".format(new_symbols))
            ev = self.subscribe_event(new_symbols)
            self.ws.send(json.dumps(ev))

        # Unsubscribe
        remove_symbols = self.subscribed_symbols - self.symbols
        if len(remove_symbols) > 0:
            self.logger.debug("Removed symbols: {}".format(remove_symbols))
            ev = self.unsubscribe_event(remove_symbols)
            self.ws.send(json.dumps(ev))

        self.subscribed_symbols = self.symbols.copy()
        self.logger.debug("Current symbols: {}".format(self.subscribed_symbols))

    @staticmethod
    def normalize_symbols(s):
        return set([el.upper() for el in s])

    @staticmethod
    def subscribe_event(symbols):
        return {
            "action": "subscribe",
            "params": {
                "symbols": ",".join(list(symbols))
            }
        }

    @staticmethod
    def unsubscribe_event(symbols):
        return {
            "action": "unsubscribe",
            "params": {
                "symbols": ",".join(list(symbols))
            }
        }


class EventReceiver(threading.Thread):
    def __init__(self, client, ping_interval=15, ping_timeout=10):
        threading.Thread.__init__(self)
        self.daemon = True
        self.client = client
        self.enabled = True
        self.ping_interval = ping_interval
        self.ping_timeout = ping_timeout

    def run(self):
        import websocket
        self.client.ws = websocket.WebSocketApp(
            self.client.url,
            on_open=self.on_open,
            on_close=self.on_close,
            on_message=self.on_message,
            on_error=self.on_error
        )

        self.client.logger.debug("EventReceiver ready")
        self.client.ws.run_forever(
            ping_interval=self.ping_interval,
            ping_timeout=self.ping_timeout,
            ping_payload='ping',
        )
        self.client.logger.debug("EventReceiver exiting")

    def on_open(self, _):
        self.client.logger.info("TDWebSocket opened!")
        self.client.on_connect()

    def on_close(self, _, close_status_code, close_msg):
        self.client.logger.info(
            "TDWebSocket closed! Close status code: {0}, close message: {1}".format(close_status_code, close_msg)
        )

    def on_error(self, _, error):
        self.client.logger.error("TDWebSocket ERROR: {}".format(error))
        self.client.self_heal()

    def on_message(self, _, message):
        event = json.loads(message)
        self.client.logger.debug("Received event: {}".format(event))

        try:
            self.client.events.put_nowait(event)
        except queue.Full:
            self.client.on_queue_full()


class EventHandler(threading.Thread):
    def __init__(self, client):
        threading.Thread.__init__(self)
        self.daemon = True
        self.client = client

    def run(self):
        self.client.logger.debug("EventHandler ready")
        while True:
            data = self.client.events.get()
            if callable(self.client.on_event):
                try:
                    self.client.on_event(data)
                except Exception as e:
                    self.client.logger.error(e)
