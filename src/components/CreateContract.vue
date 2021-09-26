
<template>
  <div class="contract">
    <div class="contract__inner">
      <div ref="create" class="create contract__block">
        <form class="create__inner" id="create-contract">
          <p class="title">Добавить договор</p>
          <input-mask v-model="newContract.fullname" :name="'fullname'"
            >ФИО клиента</input-mask
          >
          <input-mask v-model="newContract.email" :name="'email'"
            >Email клиента</input-mask
          >
          <input-mask v-model="newContract.passwd" :name="'password'"
            >Пароль клиента</input-mask
          >
          <input-mask v-model="newContract.passphrase" :name="'passphrase'"
            >Секретая фраза клиента</input-mask
          >
          <input-mask
            v-model="newContract.creditAddress"
            :name="'creditAddress'"
            >Название банка</input-mask
          >
          <input-mask
            v-model="newContract.insCompAddress"
            :name="'insCompAddress'"
            >Название страховой компании</input-mask
          >
          <input-mask v-model="newContract.creditNumber" :name="'creditNumber'"
            >Номер кредитного договора</input-mask
          >
          <input-mask
            v-model="newContract.insCompNumber"
            :name="'insCompNumber'"
            >Номер договора страхования</input-mask
          >
          <input-mask
            v-model="newContract.creditTimestamp"
            :name="'creditTimestamp'"
            >Дата кредитного договора</input-mask
          >
          <input-mask
            v-model="newContract.insCompTimestamp"
            :name="'insCompTimestamp'"
            >Дата договора страхования</input-mask
          >
          <form-button @click.prevent="createHandler">Отправить</form-button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import InputMask from '@/components/InputMask.vue'
import FormButton from '@/components/FormButton.vue'

export default {
  components: {
    InputMask,
    FormButton
  },

  data() {
    return {
      contractId: '',
      dataHidden: true,
      newContract: {
        fullname: '',
        creditAddress: '',
        creditNumber: '',
        creditTimestamp: '',
        insCompAddress: '',
        insCompNumber: '',
        insCompTimestamp: '',
      }
    }
  },

  methods: {
    createHandler() {
      console.log('request to find contract information', this.contractId)
      const loader = this.$loading.show({ container: this.$refs.create, canCancel: false })
      setTimeout(() => {
        this.dataHidden = false
        loader.hide()
      }, 500)
    },

    inputHandler(e) {
      this.contractId = e.target.value
    }
  },
}
</script>