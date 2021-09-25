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
  padding: 6px 2em;
  border: none;
  border-radius: 2em;
  font-size: 18px;
  color: #ffffff;
  background: var(--secondary);
  transition: all 0.1s ease-in-out;

  &:hover {
    background: #223c80;
  }

  &:active {
    background: #3d5799;
  }
}
</style>