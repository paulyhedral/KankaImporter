import Foundation 
import ArgumentParser
import Logging

let logger = Logger(label: "org.wanderingmonster.KankaImport")

struct KankaImport : ParsableCommand {
  @Argument(help: "The CSV file containing the data to import.")
  var csvFile : String

  @Argument(help: "The file containing the template information for importing the data.")
  var templateFile: String

  @Argument(help: "The name of the campaign to which to import the data.")
  var campaignName: String

  @Argument(help: "Kanka API key.")
  var apiKey: String

  @Option(help: "Kanka API base URL.")
  var apiURL: String = "https://kanka.io/api/1.0"

  @Option(help: "Log level")
  var logLevel: String?

  mutating func run() throws {
      logger.info("Starting import from CSV file \(csvFile) to campaign \(campaignName)...")

      guard let csv = try CSVLoader(path: csvFile)?.load() else {
        throw Errors.loading
      }

      let headers = [
        "Authorization" : "Bearer \(apiKey)",
        "Content-type" : "application/json",
      ]
  }
}

KankaImport.main()