#!/usr/bin/env python3
import subprocess
import sys
import time
import atexit

# A list to keep track of all the processes we start
running_processes = []

def cleanup():
    """
    This function is registered to run at script exit.
    It ensures all child processes are terminated.
    """
    print("Shutting down all services...")
    for p in running_processes:
        try:
            # First, try to terminate gracefully
            p.terminate()
            # Wait for a short period
            p.wait(timeout=5)
        except subprocess.TimeoutExpired:
            # If it doesn't terminate, force kill it
            print(f"Process {p.pid} did not terminate gracefully, killing.")
            p.kill()
        except Exception as e:
            print(f"Error during cleanup of process {p.pid}: {e}")
    print("All services have been shut down.")

# Register the cleanup function to be called on script exit
atexit.register(cleanup)

def run():
    """
    Starts all the necessary application servers.
    """
    # Define the commands to run
    # Command for the FastAPI server
    api_command = [
        sys.executable, "api.py",
        "--host", "0.0.0.0",
        "--port", "8012",
        "--reload"
    ]

    # Command for the main application UI
    app_command = [sys.executable, "app.py"]

    # Command for the indexing UI
    index_app_command = [sys.executable, "index_app.py"]
    
    # --- Optional: If you use the Ollama embedding proxy ---
    # Uncomment the following lines to also start the proxy
    # proxy_command = [
    #     sys.executable, "embedding_proxy.py",
    #     "--port", "11435",
    #     "--host", "http://localhost:11434"
    # ]
    # ---------------------------------------------------------

    try:
        # Start the API server
        print("Starting API server on port 8012...")
        api_process = subprocess.Popen(api_command)
        running_processes.append(api_process)
        time.sleep(2) # Give it a moment to start up

        # Start the main app UI
        print("Starting main chat UI (app.py)...")
        app_process = subprocess.Popen(app_command)
        running_processes.append(app_process)

        # Start the indexer app UI
        print("Starting indexing UI (index_app.py)...")
        index_app_process = subprocess.Popen(index_app_command)
        running_processes.append(index_app_process)
        
        # --- Optional: Start the embedding proxy ---
        # Uncomment the following lines
        # print("Starting embedding proxy on port 11435...")
        # proxy_process = subprocess.Popen(proxy_command)
        # running_processes.append(proxy_process)
        # -------------------------------------------

        print("\nAll services are running.")
        print("  - API Server: http://localhost:8012")
        print("  - Main Chat UI: http://localhost:7860 (usually)")
        print("  - Indexing UI: http://localhost:7861 (usually)")
        # print("  - Embedding Proxy: http://localhost:11435") # Uncomment if using
        print("\nPress Ctrl+C to shut down all services.")

        # Keep the main script alive, waiting for Ctrl+C
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        # The cleanup function registered with atexit will handle the shutdown
        print("\nCtrl+C detected. Initiating shutdown...")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    run()
