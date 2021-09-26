<template>
  <div class="centred">
    <div class="centred__inner">
      <div class="login">
        <div class="login__inner">
          <form @submit.prevent="loginHandler" id="login-form">
            <p class="login__header">
              {{ titles.header[authType]
              }}<span @click.stop="toMainPage"></span>
            </p>
            <!-- <img src="@/assets/gosuslugi.png" alt="" class="gosuslugi" />
            <p class="separator">Или</p> -->
            <select v-model="character" name="" id="" class="enumRole">
              <option value="bank">Банк</option>
              <option value="insurer">Страховая</option>
              <option value="person">Физ. лицо</option>
            </select>
            <input-mask
              @keydown.enter="loginHandler"
              v-if="character != 'person'"
              v-model="organization"
              :name="'organization'"
              class="login__field"
              :class="{ wrong: authError }"
              >Организация</input-mask
            >
            <input-mask
              v-model="login"
              :name="'username'"
              class="login__field"
              :class="{ wrong: authError }"
              >Логин</input-mask
            >
            <input-mask
              v-model="passwd"
              :name="'password'"
              class="login__field"
              :class="{ wrong: authError }"
              >Пароль</input-mask
            >
            <input-mask
              v-model="secret"
              :name="'passphrase'"
              class="login__field"
              :class="{ wrong: authError }"
              >Секретная фраза</input-mask
            >
            <form-button>{{ titles.button[authType] }}</form-button>
            <p @click.stop="switchType" class="switch">
              {{ titles.switch[authType] }}
            </p>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import InputMask from '@/components/InputMask.vue'
import FormButton from '@/components/FormButton.vue'
import InputMobile from '@/components/InputMobile.vue'
import { mapActions } from 'vuex'
import axios from 'axios'
import server_url from '@/env.js'

export default {
  name: 'OrderForm',

  components: {
    InputMask,
    FormButton,
    InputMobile
  },

  emits: ['submit'],

  inject: ['deleteQuery', 'addQuery'],

  setup() {
    const titles = {
      header: {
        login: 'Вход для зарегистрированных пользователей',
        registration: 'Регистрация пользователя'
      },
      button: {
        login: 'Вход',
        registration: 'Создать'
      },
      switch: {
        login: 'У меня нет аккаунта',
        registration: 'У меня уже есть аккаунт'
      }
    }

    return {
      titles
    }
  },

  mounted() {
    if (this.$route.query.logout != null) {
      console.log('logout request')
      this.updateAuthToken(undefined)
      this.updateCharacter(undefined)
    }
  },

  data() {
    return {
      login: '',
      passwd: '',
      secret: '',
      character: 'person',
      authError: false,
    }
  },

  computed: {
    authType() {
      return this.$route.query.type || 'login'
    },

    registerUrl() {
      const url = 'register'
      if (this.character == 'person')
        return url
      if (this.character == 'bank')
        return url + '_bank_user'
      return url + '_insurer_user'
    }
  },

  methods: {
    ...mapActions(['updateCharacter', 'updateAuthToken']),

    switchType() {
      if (this.authType === 'login') {
        return this.addQuery('type', 'registration')
      }
      this.deleteQuery('type')
    },

    async loginHandler() {
      const enumRole = ['bank', 'insurer', 'person']

      if (this.login.length == 0 || this.passwd.length == 0 || this.secret.length == 0)
        return this.authError = true
      if (this.authType === 'registration') {
        const status = await this.regon()
        console.log('reg state', status)
        if (status !== 200)
          return this.authError = true
      }
      const { status, token, role } = await this.logon()
      if (status !== 200)
        return this.authError = true
      this.updateAuthToken(token)
      this.updateCharacter(enumRole[role])
      this.$router.push({ name: 'profile' })
    },

    async regon() {
      const data = { login: this.login, password: this.passwd, passphrase: this.secret }
      const status = axios.post(`${server_url}/${this.registerUrl}`, data)
        .then(res => res.status)
        .catch((err, res) => err)
      return status
    },

    async logon() {
      const data = new URLSearchParams()
      data.append('username', this.login)
      data.append('password', this.passwd)
      const options = {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        }
      }
      const response = await axios.post(`${server_url}/login`, data, options)
        .then(res => {
          console.log('login', res)
          return {
            status: res.status,
            token: res.data.wallet_address,
            role: res.data.user_role,
          }
        })
        .catch((err, res) => {
          console.log('login catch', err, res)
          return res
        })
      return response
    },

    toMainPage() {
      this.$router.push({ name: 'home' })
    }
  },
}
</script>

<style lang="scss" scoped>
.centred {
  width: 100%;
  height: calc(100% - var(--h-navbar));
  overflow-y: auto;

  &__inner {
    width: 100%;
    height: 100%;
  }
}
.login {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;

  &__inner {
    position: relative;
    width: 100%;
    max-width: 540px;
    // height: 100%;
    max-height: 550px;
    border-radius: 17px;
    background-color: var(--primary-lite);
    box-shadow: 0 0 300px rgba(0, 0, 0, 0.4);
    overflow: hidden;
  }

  &__header {
    padding: 0.5em 15px;
    display: flex;
    justify-content: space-between;
    width: 100%;
    color: #fff;
    font-size: 20px;
    font-weight: 00;
    background-color: var(--secondary);

    span {
      margin-left: 5px;
      display: inline-block;
      vertical-align: middle;
      position: relative;
      height: 24px;
      width: 24px;
      border-radius: 12px;
      border: 2px solid #fff;
      cursor: pointer;

      &::before,
      &::after {
        content: "";
        display: block;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%) rotate(-45deg);
        width: 70%;
        height: 2px;
        background-color: #fff;
      }

      &::after {
        transform: translate(-50%, -50%) rotate(45deg);
      }
    }
  }

  &__field {
    width: 90%;
  }
}

.gosuslugi {
  margin: 15px 0 10px;
}

.separator {
  position: relative;
  font-size: 20px;
  width: 90%;
  color: #b4bbc3;

  &::before,
  &::after {
    position: absolute;
    content: "";
    bottom: 10%;
    right: 0;
    width: 45%;
    height: 2px;
    background-color: #b4bbc3;
    z-index: 0;
  }

  &::before {
    left: 0;
  }
}

#login-form {
  margin: auto;
  padding: 0 0 5px;
  display: flex;
  flex-flow: column nowrap;
  justify-content: flex-start;
  align-items: center;
  width: 100%;
}

.enumRole {
  margin: 15px 0;
  width: 200px;
  height: 2em;
  font-size: 20px;
  text-align: center;
  border-radius: 1em;
  border: solid 1px #dde1e6;

  &:hover {
    border: solid 1px #b4bbc3;
  }

  &:focus {
    border: solid 1px var(--secondary);
  }
}

.switch {
  margin: 10px 0;
  text-decoration: underline;
  transition: 0.25s;
  cursor: pointer;

  &:hover {
    color: var(--blue);
  }
}

@media screen and (max-width: 540px) {
  .login {
    &__inner {
      border-radius: 0;
    }
  }
}
@media screen and (max-height: 520px) {
  .login {
    align-items: flex-start;
  }
}
@media screen and (max-width: 420px) {
  #login-form {
    min-height: 100%;
  }
}
</style>