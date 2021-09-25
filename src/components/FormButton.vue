<template>
  <div class="form-button">
    <button @click.stop="submit" type="submit" class="button">
      <slot></slot>
    </button>
  </div>
</template>

<script>
export default {
  methods: {
    submit() {
      this.$emit('submit')
    }
  }
}
</script>

<style lang="scss" scoped>
.form-button {
  margin-top: 15px;
  display: flex;
  width: 100%;
}

.button {
  margin: auto;
  padding: 10px 2em;
  border: none;
  border-radius: 5px;
  font-size: 18px;
  color: #ffffff;
  background: #2045cb;
  transition: all 0.1s ease-in-out;

  &:hover {
    background: #1e41bd;
  }

  &:active {
    background: #18359c;
  }
}
</style>