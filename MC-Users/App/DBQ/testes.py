from utilizadores_db import UtilizadoresDB
from sistema import Sistema

# Create an instance of UtilizadoresDB
db = UtilizadoresDB()

# Create an instance of Sistema with the UtilizadoresDB instance
sistema = Sistema(db)

# Test the functions
sistema.registaAluno("John Doe", 1, "john@example.com")
sistema.registaDocente("Dr. Smith", 2, "smith@example.com")

# Add more test cases and assertions based on your requirements

# Print the current state of the in-memory database
print(db.users)
