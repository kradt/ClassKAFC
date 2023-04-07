from kafc import create_app


if __name__ == '__main__':
	app = create_app()
	app.run(port=80, host="0.0.0.0",)
