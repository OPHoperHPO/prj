<template>
  <div class="contract">
    <div class="contract__inner">
      <div ref="search" class="search contract__block">
        <div class="search__inner">
          <p class="title">Поиск договора</p>
          <input-mask
            @keydown.enter="searchHandler"
            v-model="contractId"
            :name="'contractId'"
            >Номер договора</input-mask
          >
          <form-button @submit="searchHandler">Найти</form-button>
        </div>
        <div v-if="!dataHidden" class="data">
          <div v-if="'role' == 'bank'" class="payment">
            <template v-for="(payment, idx) in payments" :key="idx">
              <div class="payment__item">Платежка {{ idx }}</div>
            </template>
          </div>
          <div v-else class="info">
            <div class="info__list">
              <div class="info__item">
                <p class="info__key">Дата заключения договора:</p>
                <p class="info__value">123</p>
              </div>
              <div class="info__item">
                <p class="info__key">Дата заключения договора:</p>
                <p class="info__value">123</p>
              </div>
              <div class="info__item">
                <p class="info__key">Дата заключения договора:</p>
                <p class="info__value">123</p>
              </div>
              <div class="info__item">
                <p class="info__key">Дата заключения договора:</p>
                <p class="info__value">123</p>
              </div>
              <div class="info__item">
                <p class="info__key">Дата заключения договора:</p>
                <p class="info__value">123</p>
              </div>
            </div>
            <div class="btns">
              <button class="btn">Расторгнуть контракт</button>
              <button class="btn">Сменить страховую компанию</button>
            </div>
          </div>
        </div>
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
    FormButton,
  },

  data() {
    return {
      contractId: '',
      dataHidden: true,
    }
  },

  methods: {
    searchHandler() {
      console.log('request to find contract information')
      const loader = this.$loading.show({ container: this.$refs.search, canCancel: false })
      // setTimeout(() => {
      //   this.dataHidden = false
      //   loader.hide()
      // }, 500)
    },

    inputHandler(e) {
      this.contractId = e.target.value
    }
  },
}
</script>