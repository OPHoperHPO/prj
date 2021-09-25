
<template>
  <div class="contract">
    <div class="contract__inner">
      <div ref="create" class="create contract__block">
        <form class="create__inner" id="create-contract">
          <p class="title">Страховой случай</p>
          <input-mask v-model="newContract.fullname" :name="'fullname'"
            >Страховой полис</input-mask
          >
          <input-mobile
            v-model="newContract.creditAddress"
            :name="'creditAddress'"
            >Телефон</input-mobile
          >
          <input-mask
            v-model="newContract.creditNumber"
            :name="'creditNumber'"
            :type="'email'"
            >Email</input-mask
          >
          <select name="event" id="" class="event">
            <option :value="null" selected>Выбрать</option>
            <template v-for="(evt, idx) in event_types" :key="idx">
              <option :value="evt">{{ evt }}</option>
            </template>
          </select>
          <input-mask
            v-model="newContract.creditTimestamp"
            :name="'creditTimestamp'"
            >Дата проишествия</input-mask
          >
          <form-button @click.prevent="createHandler">Заявить</form-button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import InputMask from '@/components/InputMask.vue'
import InputMobile from '@/components/InputMobile.vue'
import FormButton from '@/components/FormButton.vue'

export default {
  components: {
    InputMask,
    InputMobile,
    FormButton
  },

  setup() {
    const event_types = [
      'Повреждено застрахованное имущество',
      'Причинен ущерб третьим лицам',
      'Смерть',
      'Инвалидность',
      'Временная утрата трудоспосопности',
      'Риск прекращения / ограничения права собственности',
    ]
    
    return {
      event_types
    }
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
.event {
  padding: 16px;
  width: 100%;
  height: 100%;
  max-height: 55px;
  font-family: "Roboto";
  font-size: 16px;
  outline: none;
  border: solid 1px #dde1e6;
  border-radius: 1em;
  transition: border 0.2s ease-in-out;

  &:hover {
    border: solid 1px #b4bbc3;
  }

  &:focus {
    border: solid 1px var(--secondary);
  }
}
</style>