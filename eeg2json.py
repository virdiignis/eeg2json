import mne
import json

PROBING = 500


class eeg2json:
    def __init__(self, filename: str):
        self.file = mne.io.read_raw_brainvision(filename)
        self.filename = filename
        self.markers: dict = dict()

    def eeg2json(self):
        return json.dumps(self.file.get_data().tolist())

    def read_vmrk(self):
        with open('.'.join(self.filename.split('.')[:-1]) + '.vmrk') as F:
            lines = F.readlines()
        for l in range(len(lines)):
            try:
                if lines[l].startswith("Mk") and lines[l].split(',')[1] == "S250" != lines[l - 1].split(',')[1] \
                        and not int(lines[l - 1].split(',')[3]):
                    self.markers[lines[l - 1].split(',')[1]] = (
                        int(lines[l - 1].split(',')[2]), int(lines[l].split(',')[2]))
                try:
                    if lines[l].split(',')[1] == "S250" == lines[l - 1].split(',')[1]:
                        print("2 markers in a row signed as S250 – line {}".format(l))
                except:
                    pass
            except:
                print("Error in parsing line {}: {}".format(l, lines[l]))
        return self.markers

    def vmrk2json(self):
        self.read_vmrk()
        return json.dumps(self.markers)

    def marker2json(self, marker, stop=None):
        self.read_vmrk()
        return json.dumps(self.file.get_data(start=self.markers[marker][0],
                                             stop=self.markers[marker][0] + stop * PROBING if stop is not None else
                                             self.markers[marker][1]).tolist())


if __name__ == '__main__':
    e = eeg2json("/home/prance/Eryk/clean_m_AM1.vhdr")
    print(e.marker2json("S  1", 1))
