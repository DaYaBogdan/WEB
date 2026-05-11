import {createStore} from "vuex";
import router from "@/router";

export default createStore({
  state: {
    account: {
      verified: false,
      role: "undenified",
    },

    choosing: false,
  },
  mutations: {
    async LOGIN(state, role) {
      state.account.verified = true;
      state.account.role = role;
    },
  },
  actions: {
    async fetchAccount({commit}) {
      console.log("Начало верификации пользователя");

      const response = await fetch(
        "https://localhost:8000/api/login",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            login: login,
            password: password,
          }),
        },
      );

      const data = await response.json();

      if (data.status === 400) {
        return 400;
      }

      console.log(data.data);
      commit("LOGIN", data.data); //data.data = password

      return 0;
    },
  },
});
