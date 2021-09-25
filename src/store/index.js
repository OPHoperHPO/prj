import { createStore } from 'vuex'

export default createStore({
  state: {
    character: 'person',
    authToken: undefined,
  },
  mutations: {
    character(state, payload) {
      state.character = payload
    },
    authToken(state, payload) {
      state.authToken = payload
    }
  },
  actions: {
    updateCharacter({ commit }, payload) {
      commit('character', payload);
    },
    updateAuthToken({ commit }, payload) {
      commit('authToken', payload);
    }
  },
  getters: {
    character: (state) => state.character,
    authToken: (state) => state.authToken,
  }
})
