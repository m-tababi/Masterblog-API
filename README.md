# Masterblog API

Eine einfache RESTful API zum Verwalten von Blogposts, entwickelt mit **Flask**.  
Unterstützt CRUD-Operationen, Suche, Sortierung und API-Dokumentation über Swagger.

## 🚀 Features

- **Blogposts abrufen** (`GET /api/posts`)
- **Sortierung** nach `title` oder `content`  
  `GET /api/posts?sort=title&direction=asc`
- **Neuen Post erstellen** (`POST /api/posts`)
- **Post aktualisieren** (`PUT /api/posts/<id>`)
- **Post löschen** (`DELETE /api/posts/<id>`)
- **Search-Endpoint** (`GET /api/posts/search`)
- **Swagger API Dokumentation** unter  
  👉 `http://localhost:5002/api/docs`

## 📦 Installation

```bash
pip install flask flask-cors flask-swagger-ui
```

## ▶️ Anwendung starten

```bash
python backend_app.py
```

Standard-Port: **5002**

## 📘 Swagger Dokumentation

Nach dem Start erreichbar unter:

```
http://localhost:5002/api/docs
```

Die Spezifikation liegt unter:

```
/static/masterblog.json
```

## 📂 Projektstruktur (vereinfacht)

```
project/
│
├── backend_app.py
├── static/
│   └── masterblog.json
└── README.md
```

## 🧪 Testen der API

Die API kann mit Tools wie **Postman**, **Insomnia** oder direkt im **Swagger UI** getestet werden.

## 💡 Hinweis

Dies ist ein Lernprojekt zum Üben von REST-APIs in Flask.  
Die Daten werden in einer einfachen In-Memory-Liste gespeichert und nicht persistiert.

## 📝 Lizenz

Dieses Projekt dient zu Lernzwecken und kann frei weiterverwendet werden.
