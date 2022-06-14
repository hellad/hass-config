
try {
<<<<<<< HEAD
  new Function("import('/hacsfiles/frontend/main-f3e781b1.js')")();
} catch (err) {
  var el = document.createElement('script');
  el.src = '/hacsfiles/frontend/main-f3e781b1.js';
  el.type = 'module';
=======
  new Function("import('/hacsfiles/frontend/main-ff32767d.js')")();
} catch (err) {
  var el = document.createElement('script');
  el.src = '/hacsfiles/frontend/main-ff32767d.js';
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
  document.body.appendChild(el);
}
  