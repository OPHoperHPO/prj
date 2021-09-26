<template>
  <div class="notification">
    <div class="notification__inner">
      <div class="notification__header">
        <span class="create" @click.stop="createNotification"></span>
        <p>Оповещения</p>
        <span class="close" @click.stop="closeNotification"></span>
      </div>
      <div class="notification__list">
        <div
          v-for="(item, idx) in notifications"
          :key="idx"
          class="notification__item"
        >
          <p class="text">{{ item }}</p>
        </div>
        <p class="text" v-if="noNotifications">Список пуст</p>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  data() {
    return {
      notifications: [],
    }
  },
  
  computed: {
    noNotifications() {
      return !this.notifications || this.notifications.length == 0
    }
  },

  methods: {
    ...mapActions(['closeNotification']),

    createNotification() {
      this.notifications.push('Случайное уведомление')
    }
  }
}
</script>

<style lang="scss" scoped>
.notification {
  position: absolute;
  bottom: 10px;
  right: 10px;
  width: 300px;
  height: auto;
  border-radius: 17px;
  background-color: var(--primary-lite);
  box-shadow: var(--separator-shadow);
  overflow: hidden;

  &__inner {
  }

  &__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 2.5em;
    color: #fff;
    font-size: 18px;
    background-color: var(--secondary);

    .create,
    .close {
      position: relative;
      top: 0;
      height: 1em;
      width: 1em;
      border-radius: 1em;
      border: 2px solid #fff;
      cursor: pointer;
    }

    .create {
      margin: 0 0 0 5px;

      &::before,
      &::after {
        content: "";
        display: block;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 60%;
        height: 2px;
        background-color: #fff;
      }

      &::after {
        transform: translate(-50%, -50%) rotate(90deg);
      }
    }

    .close {
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

  &__list {
    // padding: 5px 0;
    min-height: 100px;
    max-height: 400px;
    overflow-y: auto;
  }

  &__item {
    margin: 5px auto;
    width: 90%;
    border-radius: 1em;
    border: 1px solid var(--primary-dark);

    &.active {
      border-width: 2px;
    }
  }
}
</style>