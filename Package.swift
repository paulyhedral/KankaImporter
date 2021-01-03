// swift-tools-version:5.3
// The swift-tools-version declares the minimum version of Swift required to build this package.

import PackageDescription

let package = Package(
  name: "KankaImporter",
  platforms: [
    .macOS(.v10_15)
  ],
  products: [
    // Products define the executables and libraries produced by a package, and make them visible to other packages.
    .executable(
      name: "KankaImporter",
      targets: ["KankaImporter"]
    ),
  ],
  dependencies: [
    // Dependencies declare other packages that this package depends on.
    // .package(url: /* package url */, from: "1.0.0"),
    .package(url: "https://github.com/apple/swift-argument-parser", from: "0.3.0"),
    // .package(url: "https://github.com/Alamofire/Alamofire", .upToNextMajor(from: "5.2.0")),
    .package(
      name: "Mustache", url: "https://github.com/groue/GRMustache.swift",
      .upToNextMajor(from: "4.0.0")),
    .package(url: "https://github.com/apple/swift-log", from: "1.0.0"),
    .package(url: "https://github.com/apple/swift-system", from: "0.0.1"),
    .package(url: "https://github.com/swiftcsv/SwiftCSV", from: "0.6.0"),
    .package(url: "https://github.com/paulyhedral/KankaKit", .branch("develop")),
  ],
  targets: [
    // Targets are the basic building blocks of a package. A target can define a module or a test suite.
    // Targets can depend on other targets in this package, and on products in packages which this package depends on.
    .target(
      name: "KankaImporter",
      dependencies: [
        "KankaKit",
        "Mustache",
        .product(name: "ArgumentParser", package: "swift-argument-parser"),
        .product(name: "Logging", package: "swift-log"),
        .product(name: "SystemPackage", package: "swift-system"),
        "SwiftCSV",
      ]
    ),
    .testTarget(
      name: "KankaImporterTests",
      dependencies: ["KankaImporter"]
    ),
  ]
)
