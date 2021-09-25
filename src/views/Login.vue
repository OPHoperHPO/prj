<template>
  <div class="centred login">
    <div class="login__inner">
      <form @submit.prevent="$emit('submit', $event.target)" id="login-form">
        <p class="login__header">{{ titles.header[contentType] }}</p>
        <select name="" id="" class="role">
          <option value="bank">Банк</option>
          <option value="insurer">Страховая</option>
          <option value="person">Физ. лицо</option>
        </select>
        <input-mask v-model="login" :name="'login'" class="login__field"
          >Логин</input-mask
        >
        <input-mask v-model="passwd" :name="'password'" class="login__field"
          >Пароль</input-mask
        >
        <input-mask v-model="secret" :name="'secret'" class="login__field"
          >Секретная фраза</input-mask
        >
        <form-button>{{ titles.button[contentType] }}</form-button>
        <p @click.stop="switchType" class="switch">
          {{ titles.switch[contentType] }}
        </p>
      </form>
    </div>
  </div>
</template>

<script>
import InputMask from '@/components/InputMask.vue'
import FormButton from '@/components/FormButton.vue'
import InputMobile from '@/components/InputMobile.vue'

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
        login: 'Авторизация',
        registration: 'Регистрация'
      },
      button: {
        login: 'Авторизироваться',
        registration: 'Зарегистрироваться'
      },
      switch: {
        login: 'Еще нет аккаунта?',
        registration: 'Войти в аккаунт'
      }
    }

    return {
      titles
    }
  },

  data() {
    return {
      login: '',
      passwd: '',
      secret: '',
    }
  },

  computed: {
    contentType() {
      return this.$route.query.type || 'login'
    }
  },

  methods: {
    switchType() {
      if (this.contentType === 'login') {
        return this.addQuery('type', 'registration')
      }
      this.deleteQuery('type')
    },

    submit() {
      if (contentType === 'login') {

      }
    }
  },
}
</script>

<style lang="scss" scoped>
.centred {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: calc(100% - var(--h-navbar));
}

.login {
  &__inner {
    position: relative;
    width: 100%;
    max-width: 450px;
    height: 100%;
    max-height: 550px;
    overflow: auto;
  }

  &__header {
    padding: 0.5em 0;
    width: 100%;
    // color: #fff;
    font-size: 20px;
    font-weight: 600;
  }

  &__field {
    width: 90%;
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
  border-radius: 10px;
  background-color: var(--primary-lite);
  box-shadow: var(--separator-shadow);
  overflow: hidden;
}

.role {
  margin: 15px 0;
  width: 200px;
  height: 2em;
  font-size: 20px;
  text-align: center;
  border-radius: 4px;
  border: solid 1px #dde1e6;

  &:hover {
    border: solid 1px #b4bbc3;
  }

  &:focus {
    border: solid 1px #6eaffe;
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

@media screen and (max-width: 420px) {
  #login-form {
    min-height: 100%;
  }
}
</style>