
import websocket
import json
import time
from collections import deque

symbols = ["cfxusdt", "belusdt", "kdausdt", "crvusdt", "sklusdt", "storjusdt", "maskusdt",
           "rsrusdt", "spellusdt", "superusdt", "animeusdt", "shellusdt", "dogsusdt"]

WINDOW_SECONDS = 300
PRICE_CHANGE_MIN = 2.5
PRICE_CHANGE_MAX = 4.0
VOLUME_SPIKE_THRESHOLD = 0.3
VOLUME_MULTIPLIER = 1.5

price_history = {symbol: deque() for symbol in symbols}
volume_history = {symbol: deque() for symbol in symbols}


def check_pumps():
    while True:
        now = time.time()
        for symbol in symbols:
            dq = price_history[symbol]
            vq = volume_history[symbol]

            while dq and now - dq[0][0] > WINDOW_SECONDS:
                dq.popleft()
            while vq and now - vq[0][0] > WINDOW_SECONDS:
                vq.popleft()

            if len(dq) >= 2 and len(vq) >= 2:
                old_time, old_price = dq[0]
                _, new_price = dq[-1]
                price_change = ((new_price - old_price) / old_price) * 100

                volumes = [v for _, v in vq]
                if volumes:
                    recent = volumes[-1]
                    avg = sum(volumes[:-1]) / len(volumes[:-1]) if len(volumes) > 1 else recent
                    volume_spike = (recent - avg) / avg if avg > 0 else 0

                    if PRICE_CHANGE_MIN <= price_change <= PRICE_CHANGE_MAX and                        recent > avg * VOLUME_MULTIPLIER and volume_spike >= VOLUME_SPIKE_THRESHOLD:
                        print(f"[PUMP SIGNAL] {symbol.upper()}: Price +{price_change:.2f}%, Volume spike {volume_spike*100:.2f}%")

                        dq.clear()
                        vq.clear()
        time.sleep(2)


def on_message(ws, message):
    data = json.loads(message)
    if 's' in data and 'c' in data and 'v' in data:
        symbol = data['s'].lower()
        price = float(data['c'])
        volume = float(data['v'])
        now = time.time()
        price_history[symbol].append((now, price))
        volume_history[symbol].append((now, volume))


def on_open(ws):
    payload = {
        "method": "SUBSCRIBE",
        "params": [f"{s}@ticker" for s in symbols],
        "id": 1
    }
    ws.send(json.dumps(payload))


def start_websocket():
    url = "wss://stream.binance.com:9443/ws"
    ws = websocket.WebSocketApp(url, on_message=on_message, on_open=on_open)
    ws.run_forever()


if __name__ == "__main__":
    import threading
    threading.Thread(target=check_pumps, daemon=True).start()
    start_websocket()
