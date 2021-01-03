import Foundation
import SwiftCSV

struct CSVLoader {

  private var url: URL

  init?(path: String) {
    guard let url = URL(string: path) else {
      return nil
    }

    self.url = url

  }

  func load() throws -> CSV {
    return try CSV(url: url)
  }
}
