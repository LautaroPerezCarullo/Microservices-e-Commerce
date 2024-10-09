# Set venv,context,port,directory list
$virtualEnvs = @(
    @{ Path = "catalog_service/venv/Scripts/Activate"; Context = "development"; Port = 5001; AppDir = "catalog_service" },
    @{ Path = "purchase_service/venv/Scripts/Activate"; Context = "development"; Port = 5002; AppDir = "purchase_service" },
    @{ Path = "payment_service/venv/Scripts/Activate"; Context = "development"; Port = 5003; AppDir = "payment_service" },
    @{ Path = "stock_service/venv/Scripts/Activate"; Context = "development"; Port = 5004; AppDir = "stock_service" },
    @{ Path = "e_comerce_app/venv/Scripts/Activate"; Context = "development"; Port = 5000; AppDir = "e_comerce_app" }
)

# Activate each venv, set context and run flask
foreach ($env in $virtualEnvs) {
    # Activate venv
    & $env['Path']
    Write-Output "Activated virtual environment: $($env['Path'])"

    # Set context
    $env:FLASK_CONTEXT = $env['Context']
    Write-Output "Flask context set to: $($env['Context'])"

    # Change directory
    Set-Location $env['AppDir']

    # Run app
    Start-Process -NoNewWindow -ArgumentList "app.py --port=$($env['Port'])" python
    Write-Output "Started Flask app in $($env['AppDir']) on port $($env['Port'])"

    # Return main directory
    Set-Location ..
}