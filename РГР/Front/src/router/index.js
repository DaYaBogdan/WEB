import {createRouter, createWebHistory} from "vue-router";
import ErrorPage from "@/views/templates/ErrorPage.vue";
import Login from "@/views/templates/Login.vue";
import Diary from "@/views/templates/Diary.vue";

const routes = [
  {
    path: "/:pathMatch(.*)*",
    name: "Error",
    component: ErrorPage,
  },
  {
    path: "/",
    name: "Login",
    component: Login,
  },
  {
    path: "/Diary",
    name: "Diary",
    component: Diary,
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
