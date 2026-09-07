import {createRouter, createWebHistory} from "vue-router";
import ErrorPage from "@/views/templates/ErrorPage.vue";
import Login from "@/views/templates/Login.vue";
import Diary from "@/views/templates/Diary.vue";
import Clients from "@/views/templates/Clients.vue";
import Masters from "@/views/templates/admin/Masters.vue";
import AllTasks from "@/views/templates/admin/AllTasks.vue";
import Settings from "@/views/templates/Settings.vue";
import store, {authReady} from "@/store";

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

function checkRoleAccess(userRole, allowedRoles) {
  if (!allowedRoles || allowedRoles.length === 0) return true;
  if (userRole === "admin") return true;
  return allowedRoles.includes(userRole);
}

router.beforeEach(async (to, from, next) => {
  // Wait for the initial session verification (GET /auth/me) to finish.
  // On the very first navigation this actually waits for the network;
  // on every navigation after that, authReady is already a resolved
  // promise, so this returns immediately with no extra delay or request.
  await authReady;

  const isLogged = store.getters.isLogged;
  const userRole = store.getters.userRole;

  console.log(
    `Navigating to: ${to.name}, Role: ${userRole}, IsLogged: ${isLogged}`,
  );

  if (to.meta.requiresAuth && !isLogged) {
    next({
      path: "/",
      query: {redirect: to.fullPath, message: "auth_required"},
    });
    return;
  }

  if (to.meta.guestOnly && isLogged) {
    next("/Diary");
    return;
  }

  if (to.meta.requiresAuth && to.meta.allowedRoles) {
    const hasAccess = checkRoleAccess(
      userRole,
      to.meta.allowedRoles,
    );

    if (!hasAccess) {
      console.warn(
        `Access denied for ${userRole} to ${to.name}`,
      );

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

  next();
});

router.afterEach((to, from) => {
  if (to.meta.title) {
    document.title = to.meta.title;
  }
});

export default router;
