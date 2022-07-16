import subprocess
import signal
import os


class Subprocessor:
	"""Context manager for running subprocesses"""

	def __enter__(self):
		self.processes = []
		return self

	def __exit__(self, *exception):
		self.shutdown()

		exc_type, exc_value, traceback = exception
		if exc_type:
			print(f'{exc_type}\n{exc_value}\n{traceback}')

	def shutdown(self):
		"""Sends interrupt signals until all processes complete"""
		for process in self.processes:
			process.send_signal(signal.SIGINT)
			try:
				process.wait()

			except KeyboardInterrupt:
				process.send_signal(signal.SIGINT)

			else:
				self.processes.remove(process)
				del process

		if self.processes:
			self.shutdown()

	def wait(self):
		"""Blocks until all processes complete"""
		try:
			for process in self.processes:
				process.wait()
				self.processes.remove(process)
				del process
		except KeyboardInterrupt:
			print('\nSubprocessor interrupted, exiting.')

	def run(self, *args, **kwargs):
		"""Arguments are passed to subprocess.run"""
		process = subprocess.Popen(*args, **kwargs)
		self.processes.append(process)