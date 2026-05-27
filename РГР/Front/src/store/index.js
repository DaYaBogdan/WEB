import {createStore} from "vuex";
import router from "@/router";
import api from "@/api";

export default createStore({
  state: {
    user: null,
    token: localStorage.getItem("token") || null,
  },
  getters: {
    isLogged: (state) => !!state.user,
    userRole: (state) => state.user?.role || "guest",
  },
  mutations: {
    SET_USER(state, user) {
      state.user = user;
    },
    SET_TOKEN(state, token) {
      state.token = token;
      if (token) {
        localStorage.setItem("token", token);
      } else {
        localStorage.removeItem("token");
      }
    },
    LOGOUT(state) {
      state.user = null;
      state.token = null;
      localStorage.removeItem("token");
    },
  },
  actions: {
    // Экшен для логина
    async login({commit}, credentials) {
      try {
        const response = await api.login(credentials);

        const {user, access_token} = response.data;
        commit("SET_USER", user);
        commit("SET_TOKEN", access_token);

        router.push("/dashboard");
        return Promise.resolve(user);
      } catch (error) {
        console.error("Login failed:", error);
        return Promise.reject(error);
      }
    },
    // Экшен для выхода
    async logout({commit}) {
      commit("LOGOUT");
      router.push("/login");
    },
    // Экшен для проверки и восстановления сессии (например, при загрузке приложения)
    // async restoreSession({commit}) {
    //   const token = localStorage.getItem("token");
    //   if (token) {
    //     try {
    //       const response = await api.getMe(); // запрос к /users/me
    //       commit("SET_USER", response.data);
    //       commit("SET_TOKEN", token);
    //     } catch {
    //       commit("LOGOUT");
    //     }
    //   }
    // },
  },
});
