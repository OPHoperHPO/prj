<template>
  <div class="profile">
    <div class="profile__inner">
      <!-- <div class="profile__list">
        <div class="profile__item">Поиск договора</div>
        <div v-if="'role' != 'bank'" class="profile__item">
          Добавить договор
        </div>
        <div v-if="'role' != 'person'" class="profile__item">
          Оформить страховой случай
        </div>
        <div class="profile__item"></div>
      </div> -->
      <find-contract />
      <create-contract v-if="this.character == 'bank'" />
      <insured-event v-if="this.character == 'person'" />
    </div>
  </div>
</template>

<script>
import FindContract from '@/components/FindContract.vue'
import CreateContract from '@/components/CreateContract.vue'
import InsuredEvent from '@/components/InsuredEvent.vue'

export default {
  components: {
    FindContract,
    CreateContract,
    InsuredEvent
  },

  computed: {
    character() {
      return this.$route.query.character
    }
  },
}
</script>

<style lang="scss">
.profile {
  padding: 15px;
  overflow-y: auto;

  &__inner {
    display: grid;
    grid-template-columns: 1fr 1fr;
    justify-content: flex-start;
    align-items: flex-start;
  }
}

.contract {
  margin: 10px;

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
.search {
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

  .data {
    margin: 25px 0 0;
    border-top: 1px solid var(--separator);
  }
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
.info {
  margin: 25px 0 0;

  &__list {
    margin: 0 auto;
    width: 90%;
    border-radius: 4px;
    border: 1px solid #212121;
    overflow: hidden;
  }

  &__item {
    width: 100%;
    display: flex;
    justify-content: center;

    &:not(:last-child) {
      border-bottom: 1px solid #212121;
    }
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
}
.btns {
  margin: 20px 0 0;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
  width: 100%;

  .btn {
    margin: 15px 0;
    padding: 8px 13px;
    display: block;
    color: #fff;
    font-size: 16px;
    border-radius: 8px;
    background-color: var(--primary-dark);
    border: 2px outset var(--primary-dark);
  }
}
</style>