document.getElementById('company-select').addEventListener('change', function() {
  const comp = this.value;
  const modelSel = document.getElementById('model-select');
  const fuelSel = document.getElementById('fuel-select');
  modelSel.innerHTML = '<option value="">-- Select Model --</option>';
  fuelSel.innerHTML = '<option value="">-- Select Fuel --</option>';
  fuelSel.disabled = true;

  if (!comp) {
    modelSel.disabled = true;
    return;
  }

  fetch(`/get_models?company=${encodeURIComponent(comp)}`)
    .then(res => res.json())
    .then(models => {
      models.forEach(m => {
        const opt = document.createElement('option');
        opt.value = m; opt.text = m;
        modelSel.appendChild(opt);
      });
      modelSel.disabled = false;
    });
});

document.getElementById('model-select').addEventListener('change', function() {
  const comp = document.getElementById('company-select').value;
  const model = this.value;
  const fuelSel = document.getElementById('fuel-select');
  fuelSel.innerHTML = '<option value="">-- Select Fuel --</option>';

  if (!model) {
    fuelSel.disabled = true;
    return;
  }

  fetch(`/get_fuels?company=${encodeURIComponent(comp)}&model=${encodeURIComponent(model)}`)
    .then(res => res.json())
    .then(fuels => {
      fuels.forEach(f => {
        const opt = document.createElement('option');
        opt.value = f; opt.text = f;
        fuelSel.appendChild(opt);
      });
      fuelSel.disabled = false;
    });
});
