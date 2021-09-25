<template>
  <div class="profile">
    <div class="profile__inner">
      <find-contract />
      <create-contract
        v-if="['insurer', 'bank'].includes(this.character)"
        class="profile__block"
      />
      <insured-event v-if="this.character == 'person'" class="profile__block" />
    </div>
  </div>
</template>

<script>
import FindContract from '@/components/FindContract.vue'
import CreateContract from '@/components/CreateContract.vue'
import InsuredEvent from '@/components/InsuredEvent.vue'
import { mapGetters } from 'vuex'

export default {
  components: {
    FindContract,
    CreateContract,
    InsuredEvent
  },

  computed: {
    ...mapGetters(['character']),
  },
}
</script>

<style lang="scss">
.profile {
  padding: 15px;
  height: 100%;
  background-color: var(--primary);
  background-image: url("../assets/bg.png");
  background-size: contain;
  background-position: bottom;
  background-repeat: no-repeat;
  overflow-y: auto;

  &__inner {
    display: flex;
    grid-gap: 15px;
    justify-content: space-evenly;
  }
}

.contract {
  margin: 15px 0 auto;
  padding: 15px;
  position: relative;
  width: 400px;
  border-radius: 1.2em;
  background-color: var(--primary-lite);
  box-shadow: var(--separator-shadow);
  overflow: hidden;

  &__inner {
    margin: auto;
    width: 90%;
    max-width: 320px;
  }

  &__table {
    display: grid;
    grid-template-columns: 1fr 1fr;
    justify-content: flex-start;
    align-items: center;
    width: 100%;
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

@media screen and (max-width: 740px) {
  .profile__inner {
    flex-direction: column;
    align-items: center;
  }
}
</style>