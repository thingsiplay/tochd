# Maintainer: Tuncay <mamehiscore@aol.com>
pkgname=tochd
pkgver=0.9
pkgrel=2
pkgdesc="Convert game ISO and archives to CD CHD for emulation."
arch=('any')
url="https://github.com/thingsiplay/tochd"
license=('MIT')
depends=('python3' 'p7zip' 'mame-tools')
source=("$pkgname-$pkgver.tar.gz::https://github.com/thingsiplay/$pkgname/archive/refs/tags/v$pkgver.tar.gz")

sha256sums=('ddb3912f24544ddda315a45b8b9cec8d7f24481861e557a7e87252fdbd29108a')

check() {
    cd "$pkgname-$pkgver"
    python3 "$pkgname.py" --version
}

package() {
    cd "$pkgname-$pkgver"
    install -m 755 -TD "$pkgname.py" "$pkgdir/usr/bin/${pkgname%%.*}"
}
