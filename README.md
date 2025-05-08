
# Pump Volume Bot (Railway Deploy)

Bu repo, [algosensei655](https://github.com/algosensei655) için Railway'de çalıştırılabilir bir gerçek zamanlı pump sinyal botudur.

## 🚀 Deploy Et

Aşağıdaki butona tıklayarak Railway'de tek tıkla çalıştırabilirsin:

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template/oEZXM0?referrer=algosensei655)

## 📦 Açıklama

- Binance WebSocket üzerinden anlık fiyat ve hacim izler
- Son 5 dakikada %2.5–4 fiyat artışı + %30 hacim spike varsa sinyal verir
- Railway'de 7/24 çalışabilir

## 📝 Dosyalar

- `main.py`: Bot kodu
- `requirements.txt`: Gerekli Python paketleri
- `Procfile`: Railway çalışma komutu
