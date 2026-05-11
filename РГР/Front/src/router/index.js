import {createRouter, createWebHistory} from "vue-router";
import LoginPage from "@/components/LoginPage.vue";
import ErrorPage from "@/components/ErrorPage.vue";
import OrdersPage from "@/components/OrdersPage.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "Логин",
      component: LoginPage,
    },
    {
      path: "/Orders",
      name: "Заказы",
      component: OrdersPage,
    },
    {
      path: "/:pathMatch(.*)*",
      name: "Ошибка",
      component: ErrorPage,
    },
  ],
});

export default router;
