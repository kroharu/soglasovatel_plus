from flaskr.api.api_spec import get_apispec, write_yaml_file
from flaskr import create_app

app = create_app()
app.app_context().push()

write_yaml_file(get_apispec(app))
