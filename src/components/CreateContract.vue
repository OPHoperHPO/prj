
<template>
  <div class="contract">
    <div class="contract__inner">
      <div ref="create" class="create contract__block">
        <form class="create__inner" id="create-contract">
          <p class="title">Добавить договор</p>
          <input-mask v-model="newContract.fullname" :name="'fullname'"
            >ФИО клиента</input-mask
          >
          <input-mask
            v-model="newContract.creditAddress"
            :name="'creditAddress'"
            >Название банка</input-mask
          >
          <input-mask v-model="newContract.creditNumber" :name="'creditNumber'"
            >Номер кредитного договора</input-mask
          >
          <input-mask
            v-model="newContract.creditTimestamp"
            :name="'creditTimestamp'"
            >Дата кредитного договора</input-mask
          >
          <input-mask
            v-model="newContract.insCompAddress"
            :name="'insCompAddress'"
            >Название страховой компании</input-mask
          >
          <input-mask
            v-model="newContract.insCompNumber"
            :name="'insCompNumber'"
            >Номер договора страхования</input-mask
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

<style lang="scss" scoped>
.contract {
  margin: 10px;

  &__inner {
  }

  &__table {
    display: grid;
    grid-template-columns: 1fr 1fr;
    justify-content: flex-start;
    align-items: center;
    width: 100%;
  }

  &__block {
    box-shadow: var(--separator-shadow);
  }
}
.title {
}
.create {
  padding: 15px;
  position: relative;
  border-radius: 5px;
  background-color: var(--primary-lite);
  overflow: hidden;

  &__inner {
    margin: auto;
    width: 90%;
    max-width: 320px;
  }
}
.data {
}
.payment {
  &__item {
  }
}
.info {
  margin: 30px 0 0;

  &__item {
    width: 100%;
    display: flex;
    justify-content: center;
    border: 1px solid #212121;
  }
  &__key,
  &__value {
    padding: 7px 0;
    flex: 1 1 auto;
  }
  &__key {
    font-weight: bold;
    border-right: 1px solid #212121;
  }

  &__value {
  }
}
.btns {
  margin: 20px 0 0;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
  width: 100%;

  .btn {
    margin: 15px 0;
    padding: 10px 20px;
    display: block;
    color: #fff;
    border-radius: 3px;
    background-color: var(--primary-dark);
    border: 2px outset var(--primary-dark);
  }
}
</style>