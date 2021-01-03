import ArgumentParser
import Logging

extension Logger.Level: ExpressibleByArgument {}

struct KankaImport: ParsableCommand {
  static var configuration = CommandConfiguration(
    abstract: "A utility for importing data into Kanka.",
    subcommands: [Generate.self, Import.self],
    defaultSubcommand: Import.self)

  struct Generate: ParsableCommand {
    static var configuration = CommandConfiguration(
      commandName: "generate",
      abstract: "Generate a template file to use for importing data to Kanka.")

    @Argument(help: "The type of template to generate.")
    var templateType: String

    mutating func run() throws {
      // TODO
    }
  }

  struct Import: ParsableCommand {
    static var configuration = CommandConfiguration(
      commandName: "import",
      abstract: "Import data from a source file into Kanka.")

    @Argument(help: "The CSV file containing the data to import.")
    var csvFile: String

    @Argument(help: "The file containing the template information for importing the data.")
    var templateFile: String

    @Argument(help: "The name of the campaign to which to import the data.")
    var campaignName: String

    @Option(help: "Environment variable name containing the Kanka API key.")
    var apiKey: String = "KANKA_API_KEY"

    @Option(help: "Kanka API base URL.")
    var apiURL: String = "https://kanka.io/api/1.0"

    mutating func run() throws {
      logger.info("Starting import from CSV file \(csvFile) to campaign \(campaignName)...")

      guard let csv = try CSVLoader(path: csvFile)?.load() else {
        throw Errors.loading
      }

    }
  }

  @Option(help: "Log level")
  var logLevel: Logger.Level = .info

}
