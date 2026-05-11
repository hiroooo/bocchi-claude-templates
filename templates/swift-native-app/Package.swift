// swift-tools-version: 6.1
import PackageDescription

let package = Package(
    name: "<ExampleApp>Feature",
    defaultLocalization: "ja",
    platforms: [.iOS(.v17)],
    products: [
        .library(
            name: "<ExampleApp>Feature",
            targets: ["<ExampleApp>Feature"]
        ),
        .library(
            name: "<ExampleApp>Shared",
            targets: ["<ExampleApp>Shared"]
        )
    ],
    dependencies: [
        .package(url: "https://github.com/RevenueCat/purchases-ios", from: "5.0.0"),
        .package(url: "https://github.com/getsentry/sentry-cocoa", from: "8.40.0"),
        .package(url: "https://github.com/pointfreeco/swift-dependencies", from: "1.5.0"),
        .package(url: "https://github.com/googleads/swift-package-manager-google-mobile-ads", from: "12.0.0"),
        .package(url: "https://github.com/SimplyDanny/SwiftLintPlugins", from: "0.57.0"),
        .package(url: "https://github.com/<your-github-username>/app-version-gate", from: "0.1.0")
    ],
    targets: [
        .target(
            name: "<ExampleApp>Shared"
        ),
        .target(
            name: "<ExampleApp>Feature",
            dependencies: [
                "<ExampleApp>Shared",
                .product(name: "RevenueCat", package: "purchases-ios"),
                .product(name: "RevenueCatUI", package: "purchases-ios"),
                .product(name: "Sentry", package: "sentry-cocoa"),
                .product(name: "Dependencies", package: "swift-dependencies"),
                .product(name: "GoogleMobileAds", package: "swift-package-manager-google-mobile-ads"),
                .product(name: "AppVersionGate", package: "app-version-gate")
            ],
            resources: [
                .process("Resources")
            ],
            linkerSettings: [
                .linkedFramework("GoogleMobileAds")
            ],
            plugins: [
                .plugin(name: "SwiftLintBuildToolPlugin", package: "SwiftLintPlugins")
            ]
        )
        // <ExampleApp>FeatureTests は Xcode 側のネイティブ test target として project.yml で定義。
        // SPM testTarget にすると xcodebuild の test action から直接起動できないため。
    ]
)
