const gulp = require('gulp')
const shell = require('gulp-shell')

gulp.task('python-runtests', shell.task(
  ['python runtests.py']
))
gulp.task('python3-runtests', shell.task(
  ['python3 runtests.py']
))

gulp.task('watch-python', () => {
  gulp.watch('*.py', ['python-runtests']);
})
gulp.task('watch-python3', () => {
  gulp.watch('*.py', ['python3-runtests']);
})

gulp.task('test-py', ['python-runtests', 'watch-python']);
gulp.task('test-py3', ['python3-runtests', 'watch-python3']);

gulp.task('default', ['python-runtests', 'watch-python']);
