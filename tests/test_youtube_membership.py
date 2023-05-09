import sys, os
import unittest
import pandas as pd
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core import youtube_membership 

class TestYoutube(unittest.TestCase):
    
    def test_get_members_from_csv(self):
     # Dados fictícios para teste
        fake_data = [
            {
                'Membros': 'João Silva',
                'Link do perfil': 'https://www.youtube.com/channel/UC-CQ5189EZ4hRDxwHtD7Sog',
                'Nível atual': 'Compilador',
                'Tempo total no nível (meses)': 0.5,
                'Tempo total como assinante (meses)': 0.5,
                'Última atualização': 'Virou assinante',
                'Carimbo de data/hora da última atualização': '2023-05-03T05:32:33.558-07:00'
            },
            {
                'Membros': 'Ana Maria Silva',
                'Link do perfil': 'https://www.youtube.com/channel/UC-CQ5189EZ4hRDxwHtD7Sog',
                'Nível atual': 'Compilador',
                'Tempo total no nível (meses)': 1,
                'Tempo total como assinante (meses)': 2,
                'Última atualização': 'Virou assinante',
                'Carimbo de data/hora da última atualização': '2023-04-29T07:56:41.806-07:00'
            }
        ]

        # Cria um DataFrame pandas com os dados fictícios
        fake_members_df = pd.DataFrame(fake_data)

        # Utiliza MagicMock para simular o resultado do core.youtube_membership.read_csv
        with patch('core.youtube_membership.read_csv', MagicMock(return_value=fake_members_df)):
            members_df = youtube_membership.get_members_from_csv('fake_file_path.csv')

        # Verifica se as colunas do DataFrame resultado estão corretamente renomeadas
        expected_columns = ['name', 'profile_url', 'membership_level', 'total_time_in_level', 'total_time_as_member', 'last_update', 'last_update_timestamp']
        self.assertListEqual(list(members_df[0].keys()), expected_columns)

        # Verifica se o resultado tem o mesmo número de linhas que os dados fictícios
        fake_data_new_columns = youtube_membership.rename_csv_columns(fake_members_df)
        self.assertEqual(len(members_df), len(fake_data_new_columns))


    def test_get_membership_badge_image(self):
        test_cases = [
                    (0, "new.png"),
                    (0.5, "new.png"),
                    (1, "1_month.png"),
                    (1.5, "1_month.png"),
                    (2, "2_months.png"),
                    (5.5, "2_months.png"),
                    (6, "6_months.png"),
                    (11.5, "6_months.png"),
                    (12, "12_months.png"),
                    (23.5, "12_months.png"),
                    (24, "24_months.png"),
                    (35.5, "24_months.png"),
                    (36, "36_months.png"),
                    (47.5, "36_months.png"),
                    (48, "48_months.png"),
                    (50, "48_months.png")
                ]

        for months, expected_badge_file_name in test_cases:
            badge_image_path = youtube_membership.get_membership_badge_image(months)
            expected_badge_image_path = os.path.join('assets', 'badges', expected_badge_file_name)

            self.assertEqual(badge_image_path, expected_badge_image_path)

if __name__ == '__main__':
    unittest.main()
