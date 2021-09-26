import { createStore } from 'vuex'

export default createStore({
  state: {
    character: 'person',
    authToken: undefined,
    notification: false,
  },
  mutations: {
    character(state, payload) {
      state.character = payload
    },
    authToken(state, payload) {
      state.authToken = payload
    },
    notification(state, payload) {
      state.notification = payload
    },
  },
  actions: {
    updateCharacter({ commit }, payload) {
      commit('character', payload)
    },
    updateAuthToken({ commit }, payload) {
      commit('authToken', payload)
    },
    openNotification({ commit }) {
      commit('notification', true)
    },
    closeNotification({ commit }) {
      commit('notification', false)
    },
    toggleNotification({ commit, state }) {
      commit('notification', !state.notification)
    },
  },
  getters: {
    character: (state) => state.character,
    authToken: (state) => state.authToken,
    notification: (state) => state.notification,
  }
})
