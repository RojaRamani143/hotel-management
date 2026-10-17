const menuButton = document.querySelector('.menu-toggle');
const navigation = document.querySelector('.nav-links');
menuButton?.addEventListener('click', () => {
  const open = navigation.classList.toggle('open');
  menuButton.setAttribute('aria-expanded', String(open));
});
document.querySelectorAll('.nav-links a').forEach(link => link.addEventListener('click', () => navigation?.classList.remove('open')));
const hotelSelect = document.getElementById('hotel_id');
const checkin = document.getElementById('checkin');
const checkout = document.getElementById('checkout');
const estimate = document.getElementById('estimate');
const formatMoney = number => new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(number);
function updateEstimate() {
  if (checkin.value) {
    const next = new Date(checkin.value + 'T00:00:00');
    next.setDate(next.getDate() + 1);
    const minimum = `${next.getFullYear()}-${String(next.getMonth() + 1).padStart(2, '0')}-${String(next.getDate()).padStart(2, '0')}`;
    checkout.min = minimum;
    if (checkout.value && checkout.value < minimum) checkout.value = '';
  }
  const price = Number(hotelSelect.selectedOptions[0]?.dataset.price || 0);
  const nights = checkin.value && checkout.value ? Math.round((new Date(checkout.value + 'T00:00:00') - new Date(checkin.value + 'T00:00:00')) / 86400000) : 0;
  estimate.textContent = price && nights > 0 ? `${nights} night${nights > 1 ? 's' : ''} · Estimated total: ${formatMoney(nights * price)}` : 'Select a hotel and dates to see the total.';
}
[hotelSelect, checkin, checkout].forEach(input => input?.addEventListener('change', updateEstimate));
document.querySelectorAll('[data-hotel]').forEach(button => button.addEventListener('click', () => {
  hotelSelect.value = button.dataset.hotel;
  updateEstimate();
  document.getElementById('booking').scrollIntoView({ behavior: 'smooth' });
}));
