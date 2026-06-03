import {createRouter, createWebHistory} from "vue-router";
import ErrorPage from "@/views/templates/ErrorPage.vue";
import Login from "@/views/templates/Login.vue";
import Diary from "@/views/templates/Diary.vue";
import Register from "@/views/templates/admin/Register.vue";
import AddClient from "@/views/templates/AddClient.vue";

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
    path: "/Register",
    name: "Register",
    component: Register,
  },
  {
    path: "/Diary",
    name: "Diary",
    component: Diary,
  },
  {
    path: "/AddClient",
    name: "AddClient",
    component: AddClient,
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
