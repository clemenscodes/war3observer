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
  in {
    packages = {
      ${system} = {};
    };
    devShells = {
      ${system} = {
        default = pkgs.mkShell {
          buildInputs = [
            pkgs.wineWow64Packages.stagingFull
            (pkgs.python3.withPackages (python-pkgs: [
              python-pkgs.pip
              python-pkgs.pyinstaller
            ]))
          ];
          shellHook = ''
            export WINEPREFIX="$(pwd)/.wine"
          '';
        };
      };
    };
  };
}
