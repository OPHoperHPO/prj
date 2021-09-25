<template>
  <nav :class="{ active: navbarActive }" class="nav">
    <router-link :to="{ name: 'home' }" class="nav__logo">
      <img src="@/assets/logo.png" />
    </router-link>
    <ul class="nav__block">
      <li v-if="userLoggedIn" class="redirect">
        <router-link
          :to="{ name: 'profile' }"
          class="redirect__link material-icons"
        >
          person
        </router-link>
      </li>
      <li class="redirect">
        <router-link :to="loginLink" class="redirect__link material-icons">
          {{ loginIcon }}
        </router-link>
      </li>
    </ul>
  </nav>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
export default {
  name: 'vNavbar',

  props: {
    links: {
      type: Object,
      default: {},
    },
    contacts: {
      type: Object,
      default: {},
    },
    height: {
      type: Object,
      require: false,
      default: { pc: '70px', tablet: '40px' },
    },
    // logo: {
    //   type: String,
    //   require: true,
    // },
    logoText: {
      type: String,
      require: true,
    },
  },

  data() {
    return {
      navbarActive: false,
    }
  },

  mounted() {
    const root = document.querySelector(':root')
    root.style.setProperty('--h-navbar', this.height.pc)
    root.style.setProperty('--h-navbar-tablet', this.height.tablet)
  },

  computed: {
    ...mapGetters(['authToken']),

    userLoggedIn() {
      return this.authToken != null
    },

    loginIcon() {
      if (this.userLoggedIn)
        return 'logout'
      return 'login'
    },

    loginLink() {
      const link = { name: 'login' }
      if (this.userLoggedIn)
        link.query = { logout: '' }
      return link
    }
  },

  methods: {
    ...mapActions(['updateCharacter']),

    toggleNavbar() {
      this.navbarActive = !this.navbarActive
    },

    characterHandler(e) {
      this.updateCharacter(e.target.value)
    }
  }
};
</script>

<style scoped lang="scss">
.nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  height: var(--h-navbar);
  background-color: var(--secondary);
  box-shadow: 0 1px 24px 0 rgba(0, 0, 0, 0.14);
  z-index: var(--z-navbar);

  &__logo {
    padding: 0 15px;
    display: flex;
    justify-content: flex-start;
    align-items: center;
    width: auto;
    height: 100%;

    img {
      width: auto;
      height: 50%;
      cursor: pointer;
    }
  }

  &__block {
    display: flex;
    justify-content: flex-end;
    align-items: center;
    flex: 1 1 auto;
    height: 100%;
    z-index: 2;
  }
}

.menu {
  display: none;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  height: 100%;
  box-shadow: 0 0 10px rgba(17, 17, 17, 0.55);

  &__logo {
    padding: 10px;
    font-size: 20px;
    color: var(--primary-lite);
    cursor: pointer;
  }

  &__btn {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    flex: 0 0 var(--h-navbar-tablet);
    height: 100%;
    cursor: pointer;

    &::before,
    span,
    &::after {
      content: "";
      display: block;
      width: 60%;
      height: 2px;
      border-radius: 5px;
      background: var(--primary-lite);
      transition: 0.3s;
      cursor: pointer;
    }

    span {
      margin: 5px 0;
    }

    &:hover {
      &::before,
      span,
      &::after {
        background-color: var(--primary-dark);
      }
    }
  }
}

.contact {
  margin: 0 15px 0 0;
  padding: 5px;
  cursor: pointer;

  &:hover > &__inner {
    width: var(--w-contact);
    transition: 0.3s;
  }

  &__inner {
    height: 34px;
    width: 34px;
    border-radius: 100em;
    background-color: #fff;
    transition: 0.4s 0.14s;
    overflow: hidden;
  }

  &__link {
    display: flex;
    height: 100%;
    width: 100%;
    color: #212121;
    cursor: pointer;

    .name {
      padding: 0 5px;
      display: flex;
      justify-content: center;
      align-items: center;
      flex: 1 1 auto;
      background-color: transparent;
      cursor: pointer;
    }
    .logo {
      padding: 5px;
      flex: 0 0 34px;
      background-color: var(--primary);
      border-radius: 50%;
      overflow: hidden;
      cursor: pointer;
    }
  }
}

.redirect {
  margin: 0 15px 0 0;
  padding: 2px 5px;
  position: relative;
  font-size: 18px;
  transition: 0.3s;
  cursor: pointer;

  &::after {
    content: "";
    position: absolute;
    display: block;
    bottom: -8px;
    left: 50%;
    transform: translateX(-50%);
    width: calc(100% - 10px);
    height: 1px;
    background-color: var(--primary);
    opacity: 0;
    transition: 0.3s;
  }

  &:hover {
    &:after {
      opacity: 1;
      bottom: -2px;
    }
  }

  &__link {
    color: var(--primary-lite);
    font-size: 30px;
  }
}
</style>
