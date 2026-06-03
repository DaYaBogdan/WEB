// src/sw.js - кастомный сервис-воркер для офлайн-очереди

const CACHE_NAME = "diary-v1";
const OFFLINE_QUEUE = "offline-queue";

// Установка сервис-воркера
self.addEventListener("install", (event) => {
  console.log("Service Worker установлен");
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll([
        "/",
        "/index.html",
        "/manifest.webmanifest",
      ]);
    }),
  );
  self.skipWaiting();
});

// Активация
self.addEventListener("activate", (event) => {
  console.log("Service Worker активирован");
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cache) => {
          if (cache !== CACHE_NAME) {
            console.log("Удаляем старый кеш:", cache);
            return caches.delete(cache);
          }
        }),
      );
    }),
  );
  self.clients.claim();
});

// Обработка офлайн-запросов
self.addEventListener("fetch", (event) => {
  const url = new URL(event.request.url);

  // Пропускаем не-api запросы
  if (!url.pathname.startsWith("/api/")) {
    event.respondWith(
      caches
        .match(event.request)
        .then((response) => response || fetch(event.request)),
    );
    return;
  }

  // Для DELETE запросов - сохраняем в очередь при офлайне
  if (event.request.method === "DELETE") {
    event.respondWith(
      fetch(event.request).catch(() => {
        // Сохраняем запрос в IndexedDB для выполнения позже
        return saveOfflineRequest(event.request);
      }),
    );
    return;
  }

  // Для GET запросов - пытаемся взять из кеша, если офлайн
  if (event.request.method === "GET") {
    event.respondWith(
      fetch(event.request)
        .then((response) => {
          // Кешируем успешные ответы
          const responseClone = response.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseClone);
          });
          return response;
        })
        .catch(() => {
          // Если офлайн, берем из кеша
          return caches
            .match(event.request)
            .then((cachedResponse) => {
              if (cachedResponse) {
                return cachedResponse;
              }
              // Если нет в кеше, возвращаем заглушку
              return new Response(
                JSON.stringify({
                  error:
                    "Вы офлайн. Данные будут загружены при подключении к интернету.",
                }),
                {
                  status: 503,
                  headers: {
                    "Content-Type": "application/json",
                  },
                },
              );
            });
        }),
    );
    return;
  }

  // Для остальных запросов
  event.respondWith(
    fetch(event.request).catch(() => {
      return new Response(
        JSON.stringify({
          error: "Нет подключения к интернету",
        }),
        {
          status: 503,
          headers: {"Content-Type": "application/json"},
        },
      );
    }),
  );
});

// Сохранение запроса в IndexedDB
async function saveOfflineRequest(request) {
  const db = await openDB();
  const transaction = db.transaction(
    [OFFLINE_QUEUE],
    "readwrite",
  );
  const store = transaction.objectStore(OFFLINE_QUEUE);

  store.add({
    id: Date.now(),
    url: request.url,
    method: request.method,
    timestamp: new Date().toISOString(),
  });

  // Показываем уведомление
  self.registration.showNotification("Офлайн-режим", {
    body: "Запрос на удаление сохранен. Будет выполнен при подключении к интернету.",
    icon: "/phoenix_192x192.png",
    badge: "/phoenix_144x144.png",
  });

  return new Response(
    JSON.stringify({
      queued: true,
      message:
        "Запрос сохранен для выполнения при подключении к интернету",
    }),
    {
      status: 202,
      headers: {"Content-Type": "application/json"},
    },
  );
}

// Открытие IndexedDB
function openDB() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open("OfflineQueueDB", 1);

    request.onerror = () => reject(request.error);
    request.onsuccess = () => resolve(request.result);

    request.onupgradeneeded = (event) => {
      const db = event.target.result;
      if (!db.objectStoreNames.contains(OFFLINE_QUEUE)) {
        db.createObjectStore(OFFLINE_QUEUE, {keyPath: "id"});
      }
    };
  });
}

// Восстановление офлайн-запросов при восстановлении соединения
self.addEventListener("online", async () => {
  console.log(
    "Соединение восстановлено, отправляем сохраненные запросы",
  );
  const db = await openDB();
  const transaction = db.transaction(
    [OFFLINE_QUEUE],
    "readonly",
  );
  const store = transaction.objectStore(OFFLINE_QUEUE);
  const requests = await store.getAll();

  for (const req of requests) {
    try {
      await fetch(req.url, {method: req.method});
      // Удаляем выполненный запрос
      const deleteTransaction = db.transaction(
        [OFFLINE_QUEUE],
        "readwrite",
      );
      deleteTransaction
        .objectStore(OFFLINE_QUEUE)
        .delete(req.id);
    } catch (error) {
      console.error(
        "Ошибка при выполнении сохраненного запроса:",
        error,
      );
    }
  }
});
