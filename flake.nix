{
  inputs = {
    nixpkgs = {
      url = "github:NixOS/nixpkgs/nixos-unstable";
    };
  };
  outputs = {
    self,
    nixpkgs,
    ...
  } @ inputs: let
    system = "x86_64-linux";
    pkgs = import nixpkgs {
      inherit system;
    };
    name = "war3observer";
    mkexe = pkgs.writeShellScriptBin "mkexe" ''
      wine "$PYTHON_HOME/Scripts/pyinstaller.exe" ./${name}/__main__.py \
        --noconfirm \
        --onefile \
        --clean \
        --contents-directory ${name} \
        -n ${name}
    '';
    runexe = pkgs.writeShellScriptBin "runexe" ''
      wine ./dist/${name}.exe
    '';
  in {
    packages = {
      ${system} = {};
    };
    devShells = {
      ${system} = {
        default = pkgs.mkShell {
          buildInputs = [
            (pkgs.python3.withPackages (python-pkgs:
              with python-pkgs; [
                pip
                pyinstaller
                construct
                setuptools
              ]))
            pkgs.wineWow64Packages.stagingFull
            mkexe
            runexe
          ];
          shellHook = ''
            export WINEPREFIX="$(pwd)/.wine"
            export PYTHON_HOME="$WINEPREFIX/drive_c/Program Files/Python313"
            echo "Install Python3 and Git inside wineprefix, then run install requirements.txt."
            echo "wine \"$PYTHON_HOME/python.exe\" -m pip install -r requirements.txt"
            echo "Running script below will install ${name}.exe or mkexe"
            cat $(which ${mkexe}/bin/mkexe)
            echo "To run ${name}.exe, run below script or runexe"
            cat $(which ${runexe}/bin/runexe)
          '';
        };
      };
    };
  };
}
