# Maintainer: Tuncay <mamehiscore@aol.com>
pkgname=tochd
pkgver=0.9
pkgrel=1
pkgdesc="Convert game ISO and archives to CD CHD for emulation."
arch=('any')
url="https://github.com/thingsiplay/tochd"
license=('MIT')
depends=('python3' 'p7zip' 'mame-tools')
source=("$pkgname-$pkgver.tar.gz::https://github.com/thingsiplay/$pkgname/archive/refs/tags/v$pkgver.tar.gz")
noextract=('Makefile' 'install.sh' 'uninstall.sh')

sha256sums=('3ea72f97182c6696c52503814cc16c61f33027b4534bc2d1bed39d688e57163c')

check() {
	cd "$pkgname-$pkgver"
    python3 "$pkgname.py" --version
}

package() {
	cd "$pkgname-$pkgver"
    mkdir -p "$pkgdir/usr/local/bin"
    install -m 755 -T "$pkgname.py" "$pkgdir/usr/local/bin/${pkgname%%.*}"
}
