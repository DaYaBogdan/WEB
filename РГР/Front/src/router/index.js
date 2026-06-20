import {createRouter, createWebHistory} from "vue-router";
import ErrorPage from "@/views/templates/ErrorPage.vue";
import Login from "@/views/templates/Login.vue";
import Diary from "@/views/templates/Diary.vue";
import Clients from "@/views/templates/Clients.vue";
import Masters from "@/views/templates/admin/Masters.vue";
import AllTasks from "@/views/templates/admin/AllTasks.vue";
import Settings from "@/views/templates/Settings.vue";
import store from "@/store";

// Определение прав доступа для ролей
const rolePermissions = {
  admin: ["*"], // доступ ко всему
  master: ["Diary", "Clients", "Settings"], // доступ только к этим маршрутам
};

const routes = [
  {
    path: "/:pathMatch(.*)*",
    name: "Error",
    component: ErrorPage,
    meta: {requiresAuth: false},
  },
  {
    path: "/",
    name: "Login",
    component: Login,
    meta: {requiresAuth: false, guestOnly: true},
  },
  {
    path: "/Masters",
    name: "Masters",
    component: Masters,
    meta: {requiresAuth: true, allowedRoles: ["admin"]},
  },
  {
    path: "/AllTasks",
    name: "AllTasks",
    component: AllTasks,
    meta: {requiresAuth: true, allowedRoles: ["admin"]},
  },
  {
    path: "/Diary",
    name: "Diary",
    component: Diary,
    meta: {
      requiresAuth: true,
      allowedRoles: ["master", "admin"],
    },
  },
  {
    path: "/Clients",
    name: "Clients",
    component: Clients,
    meta: {
      requiresAuth: true,
      allowedRoles: ["master", "admin"],
    },
  },
  {
    path: "/Settings",
    name: "Settings",
    component: Settings,
    meta: {
      requiresAuth: true,
      allowedRoles: ["master", "admin"],
    },
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

// Проверка доступа по роли
function checkRoleAccess(userRole, allowedRoles) {
  if (!allowedRoles || allowedRoles.length === 0) return true;
  if (userRole === "admin") return true; // админ имеет доступ ко всему
  return allowedRoles.includes(userRole);
}

router.beforeEach((to, from, next) => {
  const isLogged = store.getters.isLogged;
  const userRole = store.getters.userRole;

  console.log(
    `Navigating to: ${to.name}, Role: ${userRole}, IsLogged: ${isLogged}`,
  );

  // 1. Проверка авторизации
  if (to.meta.requiresAuth && !isLogged) {
    next({
      path: "/",
      query: {redirect: to.fullPath, message: "auth_required"},
    });
    return;
  }

  // 2. Перенаправление авторизованных с Login
  if (to.meta.guestOnly && isLogged) {
    next("/Diary");
    return;
  }

  // 3. Проверка роли
  if (to.meta.requiresAuth && to.meta.allowedRoles) {
    const hasAccess = checkRoleAccess(
      userRole,
      to.meta.allowedRoles,
    );

    if (!hasAccess) {
      console.warn(
        `Access denied for ${userRole} to ${to.name}`,
      );

      // Перенаправляем на доступную страницу в зависимости от роли
      let fallbackPath = "/";
      if (userRole === "master") {
        fallbackPath = "/Diary";
      } else if (userRole === "admin") {
        fallbackPath = "/Masters";
      }

      next({
        path: fallbackPath,
        query: {error: "access_denied"},
      });
      return;
    }
  }

  // Все проверки пройдены
  next();
});

// Опционально: после каждого перехода
router.afterEach((to, from) => {
  // Можно добавить аналитику или изменение заголовка страницы
  if (to.meta.title) {
    document.title = to.meta.title;
  }
});

export default router;
