import { createStore } from 'vuex'

export default createStore({
  state: {
    character: 'person',
  },
  mutations: {
    character(state, payload) {
      state.character = payload
    }
  },
  actions: {
    updateCharacter({ commit }, payload) {
      commit('character', payload);
    }
  },
  getters: {
    character: (state) => state.character,
  }
})
