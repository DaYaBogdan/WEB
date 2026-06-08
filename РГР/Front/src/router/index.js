import {createRouter, createWebHistory} from "vue-router";
import ErrorPage from "@/views/templates/ErrorPage.vue";
import Login from "@/views/templates/Login.vue";
import Diary from "@/views/templates/Diary.vue";
import Clients from "@/views/templates/Clients.vue";
import Masters from "@/views/templates/admin/Masters.vue";
import AllTasks from "@/views/templates/admin/AllTasks.vue";
import Settings from "@/views/templates/Settings.vue";

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
    path: "/Masters",
    name: "Masters",
    component: Masters,
  },
  {
    path: "/AllTasks",
    name: "AllTasks",
    component: AllTasks,
  },
  {
    path: "/Diary",
    name: "Diary",
    component: Diary,
  },
  {
    path: "/Clients",
    name: "Clients",
    component: Clients,
  },
  {
    path: "/Settings",
    name: "Settings",
    component: Settings,
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
