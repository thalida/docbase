class AdminFields {
  constructor() {
    this.$fieldTypeInput = document.querySelector(
      "[data-config-field-controller]",
    );
    this.$configFieldInputRows = Array.from(
      document.querySelectorAll("[data-config-field-type]"),
    ).map(($input) => $input.closest(".form-row"));

    if (!this.$fieldTypeInput || !this.$configFieldInputRows.length) {
      return;
    }

    this.$fieldTypeInput.addEventListener("change", () => {
      this.setConfigFieldDisplays();
    });

    this.setConfigFieldDisplays();
  }

  setConfigFieldDisplays($field) {
    this.hideAllConfigFields();
    this.showMatchingConfigField();
  }

  hideAllConfigFields() {
    this.$configFieldInputRows.forEach(($inputRow) => {
      $inputRow.style.display = "none";
    });
  }

  showMatchingConfigField() {
    const selectedFieldType = this.$fieldTypeInput.value;
    const $matchingField = document.querySelector(
      `[data-config-field-type="${selectedFieldType}"]`,
    );
    $matchingField.closest(".form-row").style.display = "block";
  }
}

window.addEventListener("DOMContentLoaded", () => {
  new AdminFields();
});
