<template>
  <div id="app__inner">
    <v-navbar
      :logoText="'Prometheus'"
      :height="{ pc: '60px', tablet: '40px' }"
    />
    <router-view />
  </div>
</template>

<script>
import vNavbar from '@/components/vNavbar.vue'

export default {
  name: 'App',

  components: {
    vNavbar,
  },

  provide() {
    return {
      deleteQuery: this.deleteQuery,
      addQuery: this.addQuery,
      readQuery: this.readQuery,
    }
  },

  data() {
    return {
      notify: false,
    }
  },

  methods: {
    deleteQuery(key) {
      let query = Object.assign({}, this.$route.query)
      delete query[key]
      if (Object.keys(query).length == 0) query = null

      this.$router.replace({ query })
    },

    addQuery(key, value) {
      const add = Object.fromEntries([[key, value]])
      const query = Object.assign({}, this.$route.query, add)
      this.$router.replace({ query })
    },

    readQuery(key) {
      return this.$route.query[key]
    },
  },
}
</script>

<style lang="scss">
@import "assets/scss/funcs";
@import "assets/scss/vars";
@import "@/assets/scss/null";

.material-icons {
  font-size: 2em;
}

html,
body {
  width: 100%;
  height: 100%;
  overflow: hidden;
}

#app {
  width: 100%;
  height: 100%;
  color: #212121;
  font-family: "PT Sans", "Helvetica Neue", "Roboto", Helvetica, Arial,
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  font-size: 16px;
  text-align: center;
  background-color: var(--primary-lite);
  background-image: url("assets/bg.png");
  background-size: contain;
  background-position: bottom;
  background-repeat: no-repeat;

  &__inner {
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
  }
}

.container {
  margin: 0 auto;
  padding: 0 10px;
  width: 100%;
  max-width: 1200px;
}

*::placeholder {
  color: var(--grey);
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100vw;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.3);
  z-index: var(--z-modal);
  cursor: pointer;

  & > * {
    border-radius: 2px;
    box-shadow: 0 0 2px var(--primary-dark);
    background: var(--primary-lite);
  }
}

.close {
  position: absolute;
  right: 5px;
  top: 5px;
  color: var(--secondary);
  cursor: pointer;
  z-index: 1;
}

.title {
  padding: 0 0 15px;
  text-align: center;
  font-size: 20px;
  font-weight: bold;
  width: 100%;
}
.text {
  font-size: 16px;
  text-align: center;
  line-height: 1.5em;
}
.title,
.text {
  &.left {
    text-align: left;
  }
  &.right {
    text-align: right;
  }
}

.link {
  margin: 10px 0 0;
  padding: 5px 8px;
  position: relative;
  border-radius: 3px;
  border: 1px solid var(--separator);
  cursor: pointer;

  span {
    display: none;
    cursor: inherit;
  }

  &:hover {
    span {
      padding: 0 3px;
      position: absolute;
      top: 50%;
      right: 0;
      display: block;
      text-align: center;
      transform: translateY(-50%) scale(0.7);
    }
  }
}

.material-icons-outlined {
  cursor: inherit;
}

.bounce-enter-active,
.bounce-leave-active {
  transition: opacity 0.2s ease;
}
.bounce-enter-from,
.bounce-leave-to {
  opacity: 0;
}
</style>
