<template>
  <div class="home">
    <div class="home__inner">
      <div class="welcome home__block">
        <div class="title"><img src="@/assets/welcome.png" alt="" /></div>
        <div class="subtitle">Безопастность, простота и гарантии</div>
        <router-link :to="{ name: 'login' }" class="to-login"
          >Авторизация</router-link
        >
      </div>
      <div class="image home__block">
        <img src="@/assets/family.png" alt="" />
      </div>
    </div>
  </div>
</template>

<script>
import FormButton from '@/components/FormButton.vue'

export default {
  name: 'Home',
  components: {
    FormButton
  }
}
</script>

<style lang="scss" scoped>
.home {
  width: 100%;
  height: 100%;

  &__inner {
    padding: 0 0 10% 0;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
  }

  &__block {
    margin: 0 15px;
    display: flex;
    max-width: 400px;
    flex-direction: column;
    justify-content: center;

    & > * {
      margin: 10px 0;
    }
  }
}

.welcome {
  .title {
    margin: 0;
    padding: 0;

    img {
      width: 270px;
    }
  }

  .subtitle {
    margin: 7px auto 25px;
    max-width: 220px;
    font-size: 18px;
  }
}

.image {
  grid-area: img;
}

.to-login {
  margin: 0 auto;
  padding: 12px 2em;
  width: 200px;
  color: #fff;
  font-size: 18px;
  border-radius: 1em;
  background-color: var(--secondary);
  transition: all 0.1s ease-in-out;
  cursor: pointer;

  &:hover {
    background: #223c80;
  }

  &:active {
    background: #3d5799;
  }
}

@media screen and (max-width: 740px) {
  .home {
    &__inner {
      padding: 20px 0 0;
      flex-direction: column-reverse;
      justify-content: flex-end;
    }

    .image {
      max-width: 50%;
    }
  }
}
</style>