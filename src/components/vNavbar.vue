<template>
  <nav :class="{ active: navbarActive }" class="nav">
    <router-link :to="{ name: 'home' }" class="nav__logo">
      <img :src="logo" />
    </router-link>
    <div class="menu">
      <a href="/" class="menu__logo">{{ logo_text }}</a>
      <div @click.stop="toggleNavbar" class="menu__btn"><span></span></div>
    </div>
    <ul class="nav__block">
      <template v-for="contact in contacts" :key="contact.name">
        <li class="contact">
          <div class="contact__inner">
            <router-link :href="contact.href" class="contact__link">
              <span class="logo material-icons-round">{{ contact.logo }}</span>
              <span class="name">{{ contact.name }}</span>
            </router-link>
          </div>
        </li>
      </template>
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
import { mapActions } from 'vuex';
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
    logo: {
      type: String,
      require: true,
    },
    logo_text: {
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
    userLoggedIn() {
      return this.authToken != null
    },

    loginIcon() {
      if (this.userLoggedIn)
        return 'logout'
      return 'login'
    },

    loginLink() {
      const link = { name: 'logout' }
      if (this.userLoggedIn)
        link.name = 'login'
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
    width: auto;
    height: 100%;

    img {
      width: auto;
      height: 100%;
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

@media screen and (max-width: 786px) {
  .nav {
    &.active {
      .menu {
        &__btn {
          &::before {
            transform: translateY(100%) rotate(45deg);
          }
          span {
            margin: 0;
            width: 0;
            opacity: 0.3;
          }
          &::after {
            transform: translateY(-100%) rotate(-45deg);
          }
        }
      }

      .nav__block {
        top: 0;
      }
    }

    &__logo {
      display: none;
    }

    &__block {
      padding: var(--h-navbar) 0 0;
      position: absolute;
      top: -100%;
      left: 0;
      flex-direction: column;
      justify-content: flex-start;
      width: 100%;
      height: 100%;
      font-size: 18px;
      background-color: var(--primary-dark);
      overflow-y: auto;
      transition: 0.3s;
    }
  }

  .menu {
    display: flex;
    background-color: var(--secondary);
    z-index: 3;
  }

  .contact {
    padding: 5px;

    &__inner {
      margin: 20px 0 0;
      width: var(--w-contact);
    }
  }

  .redirect {
    margin: 20px 0 0;
    font-size: 18px;

    &__link {
    }
  }
}
</style>
