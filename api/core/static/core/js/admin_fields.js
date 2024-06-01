class AdminFields {
  constructor($formset = document) {
    this.$formset = $formset;
    this.$fieldTypeInput = this.$formset.querySelector(
      "[data-config-field-controller]",
    );
    this.$configFieldInputRows = Array.from(
      this.$formset.querySelectorAll("[data-config-field-type]"),
    ).map(($input) => $input.closest(".form-row"));

    if (!this.$fieldTypeInput || !this.$configFieldInputRows.length) {
      return;
    }

    this.$fieldTypeInput.addEventListener(
      "change",
      this.handleFieldTypeChange.bind(this),
    );
    this.setConfigFieldDisplays();
  }

  handleFieldTypeChange() {
    this.setConfigFieldDisplays();
  }

  setConfigFieldDisplays($field) {
    this.hideAllConfigFields();
    this.showMatchingConfigField();
  }

  showAllConfigFields() {
    this.$configFieldInputRows.forEach(($inputRow) => {
      $inputRow.style.display = "block";
    });
  }

  hideAllConfigFields() {
    this.$configFieldInputRows.forEach(($inputRow) => {
      $inputRow.style.display = "none";
    });
  }

  showMatchingConfigField() {
    const selectedFieldType = this.$fieldTypeInput.value;
    const $matchingField = this.$formset.querySelector(
      `[data-config-field-type="${selectedFieldType}"]`,
    );
    $matchingField.closest(".form-row").style.display = "block";
  }

  destroy() {
    this.$fieldTypeInput.removeEventListener(
      "change",
      this.handleFieldTypeChange.bind(this),
    );
    this.showAllConfigFields();
  }
}

window.addEventListener("DOMContentLoaded", () => {
  const instances = {};

  instances[document] = new AdminFields(document);

  document.addEventListener("formset:added", (event) => {
    instances[event.target] = new AdminFields(event.target);
  });

  document.addEventListener("formset:removed", (event) => {
    instances[event.target].destroy();
    delete instances[event.target];
  });
});
